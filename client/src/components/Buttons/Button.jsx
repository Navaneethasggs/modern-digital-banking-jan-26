export default function Button({ children, ...props }) {
  return (
    <button
      className="px-4 py-2 rounded bg-purple-600 text-white hover:bg-purple-700"
      {...props}
    >
      {children}
    </button>
  );
}
