import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import History from "./pages/History";

export default function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <h1 className="logo">DrDejaVu</h1>
          <p className="tagline">Voice-First Health Memory</p>
          <nav>
            <NavLink to="/">Chat</NavLink>
            <NavLink to="/upload">Upload</NavLink>
            <NavLink to="/history">History</NavLink>
          </nav>
        </header>

        <div className="app-body">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
