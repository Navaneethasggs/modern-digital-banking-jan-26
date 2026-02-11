import React from "react";

const currencySymbols = {
  INR: "₹",
  USD: "$",
  EUR: "€",
  GBP: "£",
};

const AccountCard = ({
  bank,
  type,
  lastFour,
  balance,
  currency,
  addedDate,
  color,
  onViewDetails,
  onDelete,
}) => {
  const colorMap = {
    blue: "bg-blue-50 text-blue-600",
    green: "bg-green-50 text-green-600",
    orange: "bg-orange-50 text-orange-600",
    red: "bg-red-50 text-red-600",
    purple: "bg-purple-50 text-purple-600",
  };

  const symbol = currencySymbols[currency] || "$";

  return (
    <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm flex flex-col gap-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <div className={`p-3 rounded-lg ${colorMap[color] || "bg-gray-100"}`}>
          💳
        </div>
        <span className="bg-gray-100 text-gray-500 text-xs px-3 py-1 rounded-full font-medium">
          {type}
        </span>
      </div>

      <div className="mt-2">
        <h3 className="text-gray-500 text-sm font-medium">{bank}</h3>
        <p className="text-gray-400 text-xs">****{lastFour}</p>
      </div>

      <div className="my-2">
        <h2 className="text-2xl font-bold">
          {symbol} {balance.toLocaleString()}
        </h2>
        <span className="text-gray-400 text-xs font-bold uppercase">
          {currency}
        </span>
      </div>

      <div className="border-t border-gray-50 pt-4">
        <p className="text-gray-400 text-[10px] mb-4">Added {addedDate}</p>
        <div className="flex gap-2">
          <button
            onClick={onViewDetails}
            className="flex-1 py-2 text-sm font-medium border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            View Details
          </button>
          <button
            onClick={onDelete}
            className="flex-1 py-2 text-sm font-medium border border-red-200 text-red-500 rounded-lg hover:bg-red-50 transition-colors"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default AccountCard;