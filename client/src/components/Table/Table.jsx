export default function Table({ headers = [], children }) {
  return (
    <table className="w-full border border-gray-700">
      <thead>
        <tr>
          {headers.map((h) => (
            <th key={h} className="border px-3 py-2 text-left">
              {h}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>{children}</tbody>
    </table>
  );
}
