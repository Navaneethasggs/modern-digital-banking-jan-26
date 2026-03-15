import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { ArrowLeftRight, TrendingUp, RefreshCw, AlertCircle } from 'lucide-react';
import { formatCurrency, cn } from '../../../lib/utils';

// Common currencies to support
const POPULAR_CURRENCIES = [
    { code: 'USD', name: 'US Dollar', symbol: '$' },
    { code: 'EUR', name: 'Euro', symbol: '€' },
    { code: 'GBP', name: 'British Pound', symbol: '£' },
    { code: 'INR', name: 'Indian Rupee', symbol: '₹' },
    { code: 'JPY', name: 'Japanese Yen', symbol: '¥' },
    { code: 'AUD', name: 'Australian Dollar', symbol: 'A$' },
    { code: 'CAD', name: 'Canadian Dollar', symbol: 'C$' },
    { code: 'CHF', name: 'Swiss Franc', symbol: 'Fr' },
    { code: 'CNY', name: 'Chinese Yuan', symbol: '¥' },
    { code: 'SGD', name: 'Singapore Dollar', symbol: 'S$' },
];

export default function CurrencyConverter() {
    const [amount, setAmount] = useState('1000');
    const [convertedAmount, setConvertedAmount] = useState('');
    const [fromCurrency, setFromCurrency] = useState('USD');
    const [toCurrency, setToCurrency] = useState('INR');
    const [exchangeRate, setExchangeRate] = useState(null);
    const [rates, setRates] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [lastUpdated, setLastUpdated] = useState(null);

    // Fetch exchange rates
    const fetchRates = async (base) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await fetch(`https://api.exchangerate-api.com/v4/latest/${base}`);
            if (!response.ok) {
                throw new Error('Failed to fetch exchange rates');
            }
            const data = await response.json();
            setRates(data.rates);
            setExchangeRate(data.rates[toCurrency]);
            setLastUpdated(new Date().toLocaleTimeString());
        } catch (err) {
            console.error(err);
            setError('Could not connect to exchange rate service. Please try again later.');
        } finally {
            setIsLoading(false);
        }
    };

    // Initial fetch
    useEffect(() => {
        fetchRates(fromCurrency);
    }, [fromCurrency]);

    // Update exchange rate when target currency changes
    useEffect(() => {
        if (rates[toCurrency]) {
            setExchangeRate(rates[toCurrency]);
        }
    }, [toCurrency, rates]);

    // Recalculate converted amount when rate changes
    useEffect(() => {
        if (exchangeRate && amount !== '') {
            setConvertedAmount((parseFloat(amount) * exchangeRate).toFixed(2));
        } else {
            setConvertedAmount('');
        }
    }, [exchangeRate]); // Removed amount from dependencies to prevent typing overrides


    const handleAmountChange = (e) => {
        const val = e.target.value;
        setAmount(val);
        if (exchangeRate && val !== '') {
            setConvertedAmount((parseFloat(val) * exchangeRate).toFixed(2));
        } else {
            setConvertedAmount('');
        }
    };

    const handleConvertedAmountChange = (e) => {
        const val = e.target.value;
        setConvertedAmount(val);
        if (exchangeRate && exchangeRate > 0 && val !== '') {
            setAmount((parseFloat(val) / exchangeRate).toFixed(2));
        } else {
            setAmount('');
        }
    };

    const handleSwapCurrencies = () => {
        setFromCurrency(toCurrency);
        setToCurrency(fromCurrency);
        // Swap the numeric values visually too
        const temp = amount;
        setAmount(convertedAmount);
        setConvertedAmount(temp);
    };

    const currentRateValue = exchangeRate ? parseFloat(exchangeRate).toFixed(4) : '...';

    const formatAmount = (val, currency) => {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency, maximumFractionDigits: 2 }).format(val);
    }

    return (
        <div className="space-y-8 animate-in fade-in duration-500 max-w-4xl mx-auto">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Currency Converter</h1>
                    <p className="text-muted-foreground mt-1">Real-time exchange rates for global currencies</p>
                </div>
                <Button onClick={() => fetchRates(fromCurrency)} variant="outline" disabled={isLoading} className="shadow-sm">
                    <RefreshCw className={cn("h-4 w-4 mr-2", isLoading && "animate-spin")} />
                    Refresh Rates
                </Button>
            </div>

            {error ? (
                <div className="bg-destructive/10 border border-destructive/20 text-destructive rounded-xl p-6 flex flex-col items-center justify-center text-center">
                    <AlertCircle className="h-10 w-10 mb-2 opacity-80" />
                    <h3 className="text-lg font-bold mb-1">Service Unavailable</h3>
                    <p className="text-sm opacity-90 max-w-md">{error}</p>
                    <Button onClick={() => fetchRates(fromCurrency)} variant="outline" className="mt-4 border-destructive/30 hover:bg-destructive/20 text-destructive">
                        Try Again
                    </Button>
                </div>
            ) : (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2 space-y-6">
                        <Card className="border-border/50 shadow-xl overflow-visible relative">
                            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-primary/50" />
                            <CardContent className="p-8 space-y-8">

                                {/* Inputs area */}
                                <div className="flex flex-col md:flex-row gap-6 items-end relative">

                                    {/* From Currency */}
                                    <div className="flex-1 w-full space-y-3">
                                        <label className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Amount</label>
                                        <div className="relative group">
                                            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                                <span className="text-muted-foreground font-semibold">
                                                    {POPULAR_CURRENCIES.find(c => c.code === fromCurrency)?.symbol || '$'}
                                                </span>
                                            </div>
                                            <input
                                                type="number"
                                                min="0"
                                                value={amount}
                                                onChange={handleAmountChange}
                                                className="w-full bg-muted/30 border-2 border-transparent focus:border-primary/30 rounded-2xl py-4 pl-10 pr-4 text-2xl font-bold transition-all outline-none"
                                                placeholder="0.00"
                                            />
                                        </div>

                                        <select
                                            value={fromCurrency}
                                            onChange={(e) => setFromCurrency(e.target.value)}
                                            className="w-full bg-background border border-input rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary/20 transition-all outline-none cursor-pointer appearance-none"
                                        >
                                            {POPULAR_CURRENCIES.map(c => (
                                                <option value={c.code} key={`from-${c.code}`}>{c.code} - {c.name}</option>
                                            ))}
                                        </select>
                                    </div>

                                    {/* Swap Button */}
                                    <div className="flex items-center justify-center pb-[20px] md:pb-[30px] z-10 w-full md:w-auto relative group">
                                        <Button
                                            size="icon"
                                            onClick={handleSwapCurrencies}
                                            className="h-12 w-12 rounded-full shadow-lg bg-background border border-border text-foreground hover:bg-muted transition-transform hover:scale-110 md:absolute md:top-1/2 md:left-1/2 md:-translate-x-1/2 md:-translate-y-1/2 group-hover:rotate-180 duration-500"
                                        >
                                            <ArrowLeftRight className="h-5 w-5 text-primary" />
                                        </Button>
                                    </div>

                                    {/* To Currency */}
                                    <div className="flex-1 w-full space-y-3">
                                        <label className="text-sm font-bold text-muted-foreground uppercase tracking-wider">Converted To</label>
                                        <div className="relative group">
                                            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                                <span className="text-muted-foreground font-semibold">
                                                    {POPULAR_CURRENCIES.find(c => c.code === toCurrency)?.symbol || '$'}
                                                </span>
                                            </div>
                                            <input
                                                type="number"
                                                min="0"
                                                value={convertedAmount}
                                                onChange={handleConvertedAmountChange}
                                                className="w-full bg-muted/50 border-2 border-transparent focus:border-primary/30 rounded-2xl py-4 pl-10 pr-4 text-2xl font-bold transition-all outline-none"
                                                placeholder="0.00"
                                            />
                                        </div>
                                        <select
                                            value={toCurrency}
                                            onChange={(e) => setToCurrency(e.target.value)}
                                            className="w-full bg-background border border-input rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-primary/20 transition-all outline-none cursor-pointer appearance-none"
                                        >
                                            {POPULAR_CURRENCIES.map(c => (
                                                <option value={c.code} key={`to-${c.code}`}>{c.code} - {c.name}</option>
                                            ))}
                                        </select>
                                    </div>
                                </div>

                                {/* Status Bar */}
                                <div className="pt-6 border-t border-border/50 flex flex-col sm:flex-row justify-between items-center gap-4 text-sm">
                                    <div className="flex items-center gap-2 text-muted-foreground">
                                        <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
                                        Live mid-market rates
                                    </div>
                                    {lastUpdated && (
                                        <div className="text-muted-foreground">
                                            Last updated: <span className="font-medium text-foreground">{lastUpdated}</span>
                                        </div>
                                    )}
                                </div>

                            </CardContent>
                        </Card>

                        {/* Popular Conversion Quick Selects */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {[
                                { f: 'USD', t: 'EUR' },
                                { f: 'USD', t: 'GBP' },
                                { f: 'EUR', t: 'GBP' },
                                { f: 'GBP', t: 'INR' },
                            ].map((pair, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => { setFromCurrency(pair.f); setToCurrency(pair.t); }}
                                    className="bg-card hover:bg-muted/50 border border-border/50 rounded-xl p-4 text-center transition-colors shadow-sm"
                                >
                                    <div className="font-semibold text-sm">{pair.f} → {pair.t}</div>
                                </button>
                            ))}
                        </div>
                    </div>

                    <div className="space-y-6">
                        <Card className="border-border/50 shadow-md">
                            <CardHeader className="bg-muted/20 pb-4 border-b border-border/50">
                                <CardTitle className="flex items-center gap-2 text-lg">
                                    <TrendingUp className="h-5 w-5 text-primary" />
                                    Exchange Rate
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="p-6">
                                <div className="space-y-4">
                                    <div className="font-medium text-muted-foreground text-center">
                                        1 {fromCurrency} equals
                                    </div>
                                    <div className="text-4xl font-bold tracking-tight text-center text-primary">
                                        {currentRateValue} <span className="text-xl font-semibold text-foreground">{toCurrency}</span>
                                    </div>

                                    <div className="pt-4 border-t border-border/50 text-xs text-muted-foreground text-center leading-relaxed">
                                        Rates are provided for informational purposes only and do not constitute financial advice.
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </div>
            )}
        </div>
    );
}
