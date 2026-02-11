const colorByType = {
    savings: "blue",
    checking: "green",
    credit_card: "orange",
    loan: "red",
    investment: "purple",
};

const typeLabels = {
    savings: "Savings",
    checking: "Checking",
    credit_card: "Credit Card",
    loan: "Loan",
    investment: "Investment",
};

/**
 * Map an API account object to the format expected by AccountCard.
 */
export function mapAccountToCard(apiAccount) {
    const masked = apiAccount.masked_account || "****0000";
    const lastFour = masked.replace(/\*+/g, "").slice(-4) || "0000";

    return {
        id: apiAccount.id,
        bank: apiAccount.bank_name,
        type: typeLabels[apiAccount.account_type] || apiAccount.account_type,
        lastFour,
        balance: apiAccount.balance,
        currency: apiAccount.currency || "USD",
        addedDate: new Date(apiAccount.created_at).toLocaleDateString("en-GB", {
            day: "numeric",
            month: "short",
            year: "numeric",
        }),
        color: colorByType[apiAccount.account_type] || "blue",
    };
}

/**
 * Compute account summary from a list of mapped accounts.
 */
export function computeSummary(accounts) {
    const totalAssets = accounts
        .filter((a) => a.type !== "Credit Card" && a.type !== "Loan")
        .reduce((sum, a) => sum + a.balance, 0);

    const totalLiabilities = accounts
        .filter((a) => a.type === "Credit Card" || a.type === "Loan")
        .reduce((sum, a) => sum + a.balance, 0);

    return {
        totalAssets,
        totalLiabilities,
        netWorth: totalAssets - totalLiabilities,
        totalAccounts: accounts.length,
    };
}
