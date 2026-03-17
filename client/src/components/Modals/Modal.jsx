export default function Modal({ open, children }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
      <div className="bg-gray-900 p-6 rounded">{children}</div>
    </div>
  );
}
