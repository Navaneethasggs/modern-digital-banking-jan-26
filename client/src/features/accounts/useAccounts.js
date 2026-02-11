import { useState, useEffect, useCallback } from "react";
import {
  fetchAccounts,
  createAccount,
  deleteAccount,
} from "./AccountsAPI";
import { mapAccountToCard, computeSummary } from "./AccountsService";

export function useAccounts() {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadAccounts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const { data } = await fetchAccounts();
      setAccounts(data.map(mapAccountToCard));
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load accounts");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadAccounts();
  }, [loadAccounts]);

  const addAccount = useCallback(
    async (accountData) => {
      await createAccount(accountData);
      await loadAccounts();
    },
    [loadAccounts]
  );

  const removeAccount = useCallback(
    async (id) => {
      await deleteAccount(id);
      await loadAccounts();
    },
    [loadAccounts]
  );

  const summary = computeSummary(accounts);

  return { accounts, loading, error, addAccount, removeAccount, summary, reload: loadAccounts };
}