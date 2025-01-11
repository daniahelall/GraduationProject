import React, { useEffect, useState } from 'react';
import './DashboardPage.css';

const DashboardPage = () => {
    const [stats, setStats] = useState({
        teacher_count: 0,
        worker_count: 0,
        student_count: 0,
    });

    useEffect(() => {
        // Fetch statistics from the backend
        const fetchStats = async () => {
            try {
                const response = await fetch('http://localhost:5000/stats'); 
                const data = await response.json();
                if (response.ok) {
                    setStats(data);
                } else {
                    console.error("Error fetching stats:", data);
                }
            } catch (error) {
                console.error("Error:", error);
            }
        };

        fetchStats();

        // Poll the server every 5 seconds for real-time updates
        const interval = setInterval(fetchStats, 5000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="dashboard-container">
            <h1>Dashboard</h1>
            <div className="statistics">
                <h2>Statistics</h2>
                <p>Teachers: {stats.teacher_count}</p>
                <p>Workers: {stats.worker_count}</p>
                <p>Students: {stats.student_count}</p>
            </div>
        </div>
    );
};

export default DashboardPage;
