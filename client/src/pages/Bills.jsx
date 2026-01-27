import { useBills } from "../features/bills";

export default function Bills() {
  const { bills } = useBills();

  return (
    <div>
      <h1>Bills Page</h1>
      <p>Total bills: {bills.length}</p>
    </div>
  );
}
