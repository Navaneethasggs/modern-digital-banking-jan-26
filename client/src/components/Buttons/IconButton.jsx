export default function IconButton({ icon, ...props }) {
  return (
    <button className="p-2 rounded hover:bg-gray-700" {...props}>
      {icon}
    </button>
  );
}
