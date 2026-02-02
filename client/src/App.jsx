import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import AdminLogin from "./pages/AdminLogin";

import Dashboard from "./pages/Dashboard";
import Accounts from "./pages/Accounts";
import Transactions from "./pages/Transactions";
import Budgets from "./pages/Budgets";
import Bills from "./pages/Bills";
import Rewards from "./pages/Rewards";
import Insights from "./pages/Insights";
import Alerts from "./pages/Alerts";

import PageContainer from "./layout/PageContainer";

const withLayout = (Component) => (
  <PageContainer>
    <Component />
  </PageContainer>
);

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public */}
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/admin/login" element={<AdminLogin />} />

        {/* Dashboard */}
        <Route path="/dashboard" element={withLayout(Dashboard)} />
        <Route path="/accounts" element={withLayout(Accounts)} />
        <Route path="/transactions" element={withLayout(Transactions)} />
        <Route path="/budgets" element={withLayout(Budgets)} />
        <Route path="/bills" element={withLayout(Bills)} />
        <Route path="/rewards" element={withLayout(Rewards)} />
        <Route path="/insights" element={withLayout(Insights)} />
        <Route path="/alerts" element={withLayout(Alerts)} />
      </Routes>
    </BrowserRouter>
  );
}
