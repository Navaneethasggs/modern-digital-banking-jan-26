import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

export default function PageContainer({ children }) {
  return (
    <div className="min-h-screen bg-black text-white">
      <Navbar />

      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  );
}
