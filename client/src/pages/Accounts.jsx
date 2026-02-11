import React, { useState } from "react";
import Sidebar from "../layout/Sidebar";
import Topbar from "../layout/Navbar";
import AccountCard from "../layout/Accountcard";
import AccountsSummary from "../layout/AccountsSummary";
import { useAccounts } from "../features/accounts";

const Accounts = () => {
  const { accounts, loading, error, addAccount, removeAccount, summary } =
    useAccounts();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [addError, setAddError] = useState("");
  const [addLoading, setAddLoading] = useState(false);

  const handleAddAccount = async (e) => {
    e.preventDefault();
    setAddError("");
    setAddLoading(true);
    const formData = new FormData(e.target);
    try {
      await addAccount({
        bank_name: formData.get("bank_name"),
        account_type: formData.get("account_type"),
        masked_account: `****${Math.floor(1000 + Math.random() * 9000)}`,
        currency: formData.get("currency") || "USD",
        balance: parseFloat(formData.get("balance")) || 0,
      });
      setIsModalOpen(false);
    } catch (err) {
      setAddError(err.response?.data?.detail || "Failed to add account");
    } finally {
      setAddLoading(false);
    }
  };

  const handleDeleteAccount = async (id) => {
    if (!window.confirm("Are you sure you want to delete this account?")) return;
    try {
      await removeAccount(id);
      setSelectedAccount(null);
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to delete account");
    }
  };

  return (
    <div className="flex bg-gray-50 min-h-screen font-sans">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Topbar />
        <main className="p-10">
          <div className="flex justify-between items-center mb-2">
            <h1 className="text-2xl font-bold text-gray-800">Accounts</h1>
            <button
              onClick={() => setIsModalOpen(true)}
              className="bg-purple-600 text-white px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-purple-700 transition-colors"
            >
              <span className="text-xl">+</span> Add Account
            </button>
          </div>
          <p className="text-gray-400 mb-8">Manage your bank accounts</p>

          {/* Loading state */}
          {loading && (
            <div className="flex items-center justify-center py-20">
              <div className="flex flex-col items-center gap-3">
                <div className="w-8 h-8 border-4 border-purple-600 border-t-transparent rounded-full animate-spin" />
                <p className="text-gray-400">Loading accounts...</p>
              </div>
            </div>
          )}

          {/* Error state */}
          {error && !loading && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl mb-6">
              {error}
            </div>
          )}

          {/* Empty state */}
          {!loading && !error && accounts.length === 0 && (
            <div className="bg-white border border-gray-100 rounded-2xl p-12 text-center shadow-sm mb-8">
              <div className="text-5xl mb-4">🏦</div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                No accounts yet
              </h3>
              <p className="text-gray-400 mb-6">
                Add your first bank account to get started
              </p>
              <button
                onClick={() => setIsModalOpen(true)}
                className="bg-purple-600 text-white px-6 py-2.5 rounded-xl hover:bg-purple-700 transition-colors"
              >
                + Add Account
              </button>
            </div>
          )}

          {/* Accounts grid */}
          {!loading && accounts.length > 0 && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                {accounts.map((acc) => (
                  <AccountCard
                    key={acc.id}
                    {...acc}
                    onViewDetails={() => setSelectedAccount(acc)}
                    onDelete={() => handleDeleteAccount(acc.id)}
                  />
                ))}
              </div>
              <AccountsSummary {...summary} />
            </>
          )}
        </main>
      </div>

      {/* --- ADD ACCOUNT MODAL --- */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-2xl w-96 shadow-xl">
            <h2 className="text-xl font-bold mb-4">Add New Account</h2>

            {addError && (
              <div className="bg-red-50 border border-red-200 text-red-600 text-sm px-3 py-2 rounded-lg mb-4">
                {addError}
              </div>
            )}

            <form onSubmit={handleAddAccount} className="flex flex-col gap-4">
              <input
                name="bank_name"
                placeholder="Bank Name (e.g. Chase)"
                className="border p-2.5 rounded-lg focus:outline-none focus:border-purple-500"
                required
              />
              <select
                name="account_type"
                className="border p-2.5 rounded-lg focus:outline-none focus:border-purple-500"
              >
                <option value="savings">Savings</option>
                <option value="checking">Checking</option>
                <option value="credit_card">Credit Card</option>
                <option value="loan">Loan</option>
                <option value="investment">Investment</option>
              </select>
              <select
                name="currency"
                className="border p-2.5 rounded-lg focus:outline-none focus:border-purple-500"
              >
                <option value="USD">USD ($)</option>
                <option value="INR">INR (₹)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
              </select>
              <input
                name="balance"
                type="number"
                step="0.01"
                placeholder="Initial Balance"
                className="border p-2.5 rounded-lg focus:outline-none focus:border-purple-500"
                required
              />
              <div className="flex gap-2 mt-2">
                <button
                  type="button"
                  onClick={() => {
                    setIsModalOpen(false);
                    setAddError("");
                  }}
                  className="flex-1 py-2.5 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={addLoading}
                  className="flex-1 py-2.5 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
                >
                  {addLoading && (
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  )}
                  {addLoading ? "Saving..." : "Save"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* --- VIEW DETAILS MODAL --- */}
      {selectedAccount && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-2xl w-96 shadow-xl text-center">
            <div className="text-4xl mb-4">🏦</div>
            <h2 className="text-xl font-bold">{selectedAccount.bank}</h2>
            <p className="text-gray-500 mb-4">
              {selectedAccount.type} Account
            </p>
            <div className="bg-gray-50 p-4 rounded-xl mb-6">
              <p className="text-sm text-gray-400">Current Balance</p>
              <p className="text-2xl font-bold text-purple-600">
                {selectedAccount.currency === "INR" ? "₹" : "$"}{" "}
                {selectedAccount.balance.toLocaleString()}
              </p>
            </div>
            <p className="text-gray-400 text-xs mb-4">
              Account ****{selectedAccount.lastFour} · Added{" "}
              {selectedAccount.addedDate}
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => handleDeleteAccount(selectedAccount.id)}
                className="flex-1 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors"
              >
                Delete
              </button>
              <button
                onClick={() => setSelectedAccount(null)}
                className="flex-1 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Accounts;