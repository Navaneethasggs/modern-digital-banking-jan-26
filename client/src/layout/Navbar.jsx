export default function Navbar() {
  return (
    <nav className="h-14 w-full bg-gray-900 text-white flex items-center justify-between px-6 border-b border-gray-700">
      <span className="font-semibold text-lg text-purple-400">
        NeoVault
      </span>

      <button className="text-sm bg-purple-600 hover:bg-purple-700 px-4 py-1 rounded">
        Logout
      </button>
    </nav>
  );
}
