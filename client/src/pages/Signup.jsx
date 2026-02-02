import { Link } from "react-router-dom";

export default function Signup() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center gap-4 w-full">
      <h1 className="text-2xl">User Signup</h1>

      <input
        type="text"
        placeholder="Full Name"
        className="w-72 px-4 py-2 rounded bg-gray-800 border border-gray-600 focus:outline-none"
      />

      <input
        type="email"
        placeholder="Email"
        className="w-72 px-4 py-2 rounded bg-gray-800 border border-gray-600 focus:outline-none"
      />

      <input
        type="password"
        placeholder="Password"
        className="w-72 px-4 py-2 rounded bg-gray-800 border border-gray-600 focus:outline-none"
      />

      <button className="w-72 bg-purple-600 hover:bg-purple-700 py-2 rounded">
        Sign Up
      </button>

      <Link to="/" className="text-purple-400 hover:underline">
        Already have an account? Login
      </Link>
    </div>
  );
}
