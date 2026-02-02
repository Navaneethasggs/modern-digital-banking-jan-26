import { NavLink } from "react-router-dom";

const linkClass = ({ isActive }) =>
  `block px-2 py-1 rounded ${
    isActive
      ? "bg-gray-800 text-purple-400"
      : "hover:text-purple-400"
  }`;

export default function Sidebar() {
  return (
    <aside className="w-56 bg-gray-900 border-r border-gray-700 min-h-[calc(100vh-56px)] p-4">
      <ul className="space-y-2 text-sm">
        <li><NavLink to="/dashboard" className={linkClass}>Dashboard</NavLink></li>
        <li><NavLink to="/accounts" className={linkClass}>Accounts</NavLink></li>
        <li><NavLink to="/transactions" className={linkClass}>Transactions</NavLink></li>
        <li><NavLink to="/budgets" className={linkClass}>Budgets</NavLink></li>
        <li><NavLink to="/bills" className={linkClass}>Bills</NavLink></li>
        <li><NavLink to="/rewards" className={linkClass}>Rewards</NavLink></li>
        <li><NavLink to="/insights" className={linkClass}>Insights</NavLink></li>
        <li><NavLink to="/alerts" className={linkClass}>Alerts</NavLink></li>
      </ul>
    </aside>
  );
}
