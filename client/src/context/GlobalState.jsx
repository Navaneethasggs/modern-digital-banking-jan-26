import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../api/axios';
import { useAuth } from './AuthContext';

const GlobalContext = createContext(null);

export const GlobalProvider = ({ children }) => {
    const { isAuthenticated } = useAuth();
    const [accounts, setAccounts] = useState([]);
    const [transactions, setTransactions] = useState([]);
    const [budgets, setBudgets] = useState([]);
    const [bills, setBills] = useState([]);
    const [rewards, setRewards] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchData = async () => {
        if (!isAuthenticated) return;
        setLoading(true);
        try {
            const [accRes, txnRes, billRes, rewardRes] = await Promise.all([
                api.get('/accounts/'),
                api.get('/transactions/'),
                api.get('/bills/'),
                api.get('/bills/rewards')
            ]);
            setAccounts(accRes.data);
            setTransactions(txnRes.data);
            setBills(billRes.data);
            setRewards(rewardRes.data);

            // Fetch current month's budgets
            const today = new Date();
            const budgetRes = await api.get('/budgets/', {
                params: { month: today.getMonth() + 1, year: today.getFullYear() }
            });
            setBudgets(budgetRes.data);

        } catch (error) {
            console.error("Error fetching data", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (isAuthenticated) {
            fetchData();
        }
    }, [isAuthenticated]);

    return (
        <GlobalContext.Provider value={{
            accounts,
            transactions,
            budgets,
            bills,
            rewards,
            loading,
            refreshData: fetchData
        }}>
            {children}
        </GlobalContext.Provider>
    );
};

export const useGlobal = () => useContext(GlobalContext);
