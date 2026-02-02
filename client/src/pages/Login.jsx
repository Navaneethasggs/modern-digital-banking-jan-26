import { Link } from "react-router-dom";

export default function Login() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center gap-4 w-full">
      <h1 className="text-2xl">User Login</h1>

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
        Login
      </button>

      <Link to="/signup" className="text-purple-400 hover:underline">
        New user? Sign up
      </Link>
    </div>
  );
}
