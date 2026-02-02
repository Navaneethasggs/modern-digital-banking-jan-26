export default function Input({ label, ...props }) {
  return (
    <div className="flex flex-col gap-1">
      {label && <label className="text-sm">{label}</label>}
      <input
        className="px-3 py-2 rounded bg-gray-800 border border-gray-700"
        {...props}
      />
    </div>
  );
}
