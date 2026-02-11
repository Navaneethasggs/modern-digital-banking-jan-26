import React from "react";
import { useAuth } from "../features/auth";

const Topbar = () => {
  const { user, logout } = useAuth();

  // Get initials from user name
  const initials = user?.name
    ? user.name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2)
    : "?";

  return (
    <div className="h-16 flex items-center justify-between px-8 bg-white border-b border-gray-50">
      <div className="relative w-1/2">
        <input
          type="text"
          placeholder="Search transactions, accounts..."
          className="w-full bg-gray-50 border border-gray-200 rounded-lg py-2 px-10 focus:outline-none focus:border-purple-400 transition-colors"
        />
        <span className="absolute left-3 top-2.5 text-gray-400">🔍</span>
      </div>
      <div className="flex items-center gap-6">
        <div className="relative">
          <button className="text-gray-500 text-xl hover:text-gray-700 transition-colors">
            🔔
          </button>
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center">
            3
          </span>
        </div>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
            {initials}
          </div>
          <div className="hidden md:block">
            <p className="text-sm font-medium text-gray-700">
              {user?.name || "User"}
            </p>
            <p className="text-xs text-gray-400">{user?.email || ""}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Topbar;