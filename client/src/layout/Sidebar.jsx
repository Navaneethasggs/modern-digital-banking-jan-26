import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../features/auth";

const Sidebar = () => {
  const location = useLocation();
  const { logout } = useAuth();

  const menuItems = [
    { name: "Dashboard", icon: "📊", path: "/dashboard" },
    { name: "Accounts", icon: "💳", path: "/accounts" },
    { name: "Transactions", icon: "💸", path: "/transactions" },
    { name: "Budgets", icon: "📅", path: "/budgets" },
    { name: "Bills & Reminders", icon: "💵", path: "/bills" },
    { name: "Rewards", icon: "🎁", path: "/rewards" },
    { name: "Alerts", icon: "🔔", path: "/alerts" },
  ];

  return (
    <div className="w-64 h-screen bg-white border-r border-gray-100 flex flex-col p-4 sticky top-0">
      {/* Logo */}
      <Link to="/dashboard" className="flex items-center gap-2 mb-10 px-2">
        <div className="bg-purple-600 text-white p-1 rounded-lg">N</div>
        <span className="font-bold text-xl">NeoVault</span>
      </Link>

      {/* Nav */}
      <nav className="flex-1">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.name}
              to={item.path}
              className={`flex items-center gap-3 p-3 rounded-xl mb-1 transition-colors ${isActive
                  ? "bg-purple-600 text-white"
                  : "text-gray-500 hover:bg-gray-50"
                }`}
            >
              <span>{item.icon}</span>
              <span className="font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Logout */}
      <button
        onClick={logout}
        className="flex items-center gap-3 p-3 rounded-xl text-gray-500 hover:bg-red-50 hover:text-red-600 transition-colors mt-auto"
      >
        <span>🚪</span>
        <span className="font-medium">Logout</span>
      </button>
    </div>
  );
};

export default Sidebar;