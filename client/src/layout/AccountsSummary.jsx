import React from 'react';

const AccountsSummary = ({ totalAssets, totalLiabilities, netWorth, totalAccounts }) => {
  return (
    <div className="bg-white border border-gray-100 rounded-2xl p-8 shadow-sm">
      <h3 className="text-gray-700 font-bold mb-6">Account Summary</h3>
      <div className="grid grid-cols-4 gap-8">
        <div>
          <p className="text-gray-400 text-sm mb-1">Total Assets</p>
          <p className="text-green-500 text-xl font-bold">₹ {totalAssets.toLocaleString('en-IN')}</p>
        </div>
        <div>
          <p className="text-gray-400 text-sm mb-1">Total Liabilities</p>
          <p className="text-red-400 text-xl font-bold">₹ {totalLiabilities.toLocaleString('en-IN')}</p>
        </div>
        <div>
          <p className="text-gray-400 text-sm mb-1">Net Worth</p>
          <p className="text-gray-800 text-xl font-bold">₹ {netWorth.toLocaleString('en-IN')}</p>
        </div>
        <div>
          <p className="text-gray-400 text-sm mb-1">Total Accounts</p>
          <p className="text-gray-800 text-xl font-bold">{totalAccounts}</p>
        </div>
      </div>
    </div>
  );
};

export default AccountsSummary;