from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
# Update with your MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/student_alumni_db"
mongo = PyMongo(app)


@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    # Get student profile data from the request
    student_profile = request.json
    student_school_college = student_profile['school_college']
    student_preferred_domain = student_profile['preferred_domain']
    student_skills = set(student_profile['skills'])

    # Get pagination parameters
    page = int(request.args.get('page', 1))
    per_page = 9  # Number of recommendations per page

    # MongoDB aggregation pipeline
    pipeline = [
        {
            "$match": {
                "school_college": student_school_college,
                "domain": student_preferred_domain
            }
        },
        {
            "$addFields": {
                "skill_overlap": {
                    "$size": {
                        "$setIntersection": ["$skills", list(student_skills)]
                    }
                }
            }
        },
        {
            "$sort": {
                "skill_overlap": -1,  # Sort by skill overlap in descending order
                "updated_at": -1      # Sort by recency of update in descending order
            }
        },
        {
            "$skip": (page - 1) * per_page  # Skip documents for pagination
        },
        {
            "$limit": per_page  # Limit the number of results per page
        }
    ]

    # Execute the aggregation pipeline
    recommendations = list(mongo.db.alumni.aggregate(pipeline))

    # Return the recommendations as JSON
    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(debug=True)
