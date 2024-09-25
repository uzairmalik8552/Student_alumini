// app/(auth)/login/page.tsx

"use client";

import React, { useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";

const LoginForm = ({ role }: { role: "Student" | "Alumni" }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isOtpModalOpen, setOtpModalOpen] = useState(false);
  const router = useRouter();
const API_BASE_URL = process.env.IP_ADDR;
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);

    const res = await signIn("credentials", {
      username,
      password,
    });

    if (res?.error) {
      setError("Invalid username or password.");
    } else {
      setOtpModalOpen(true);
    }
  };

  const handleVerifyOtp = async () => {
    try {
      const response = await fetch("/api/auth/verify-otp", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, otp }),
      });

      const data = await response.json();

      if (response.ok) {
        router.push(`/${role.toLowerCase()}-dashboard`);
      } else {
        setError(data.message || "OTP verification failed.");
      }
    } catch (err) {
      setError("Error verifying OTP.");
    }
  };

  return (
    <div className="w-full max-w-md p-8 bg-base max-h-md rounded shadow-md">
      <h2 className="text-2xl font-bold text-center mb-6">{role} Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="username" className="label">
            <span className="label-text">Email</span>
          </label>
          <input
            type="text"
            id="username"
            className="input input-bordered w-full"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label className="label" htmlFor="password">
            <span className="label-text">Password</span>
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input input-bordered w-full"
          />
        </div>
        {error && <p className="text-red-500">{error}</p>}
        <button className="btn btn-primary w-full mt-4" type="submit">
          Login
        </button>
      </form>

      {/* OTP Modal */}
      {isOtpModalOpen && (
        <div className="modal">
          <div className="modal-box">
            <h3 className="font-bold text-lg">Enter OTP</h3>
            <input
              type="text"
              className="input input-bordered w-full mt-4"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
            />
            <div className="modal-action">
              <button onClick={handleVerifyOtp} className="btn">
                Verify OTP
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LoginForm;
