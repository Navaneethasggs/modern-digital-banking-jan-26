import { useTransactions } from "../features/transactions";

export default function Transactions() {
  const { transactions } = useTransactions();
  return <p>Total transactions: {transactions.length}</p>;
}
