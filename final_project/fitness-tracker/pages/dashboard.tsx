import { useState } from 'react';

export default function Dashboard() {
  const [calories, setCalories] = useState<number>(0);

  return (
    <div className="min-h-screen bg-gray-100 p-5">
      <header className="flex justify-between items-center bg-white shadow-md p-5 rounded-lg">
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <nav>
          <a href="/" className="text-blue-500 hover:underline">Home</a>
        </nav>
      </header>

      <main className="mt-10">
        <section className="bg-white shadow-md rounded-lg p-5 mb-5">
          <h2 className="text-xl font-semibold text-gray-800">Calorie Tracker</h2>
          <div className="mt-3 flex items-center justify-between">
            <p className="text-gray-600">Calories consumed today:</p>
            <span className="text-lg font-bold text-gray-800">{calories} kcal</span>
          </div>
          <button
            className="mt-5 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            onClick={() => setCalories(calories + 100)}
          >
            Add 100 kcal
          </button>
        </section>

        <section className="bg-white shadow-md rounded-lg p-5">
          <h2 className="text-xl font-semibold text-gray-800">Workout Planner</h2>
          <ul className="mt-3 text-gray-600">
            <li>- Morning Yoga: 30 mins</li>
            <li>- Cardio: 45 mins</li>
            <li>- Strength Training: 1 hour</li>
          </ul>
        </section>
      </main>
    </div>
  );
}