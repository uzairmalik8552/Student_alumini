import { MongoClient } from "mongodb";

const MONGODB_URI = process.env.MONGODB_URI;
let clientPromise: Promise<MongoClient>;

if (!MONGODB_URI) {
  throw new Error("Please define the MONGODB_URI environment variable.");
}

// Connect to MongoDB
clientPromise = MongoClient.connect(MONGODB_URI);

export async function POST(req: Request) {
  const { username, otp } = await req.json();
  const client = await clientPromise;
  const usersCollection = client.db().collection("users");

  // Find the user by email
  const user = await usersCollection.findOne({ email: username });

  if (!user || user.otp !== otp) {
    return new Response(JSON.stringify({ message: "Invalid OTP" }), { status: 401 });
  }

  // OTP is correct, clear the OTP from the database
  await usersCollection.updateOne(
    { email: username },
    { $unset: { otp: "", otpCreatedAt: "" } }
  );

  return new Response(JSON.stringify({ message: "OTP verified successfully" }), { status: 200 });
}
