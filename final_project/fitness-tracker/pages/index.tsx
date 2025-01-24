import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100 p-5">
      <header className="flex justify-between items-center bg-white shadow-md p-5 rounded-lg">
        <h1 className="text-2xl font-bold text-gray-800">Fitness Tracker</h1>
        <nav>
          <Link href="/dashboard">
            <a className="text-blue-500 hover:underline">Dashboard</a>
          </Link>
        </nav>
      </header>

      <main className="mt-10">
        <div className="text-center">
          <h2 className="text-xl font-semibold">Welcome to your fitness journey!</h2>
          <p className="text-gray-600">Track your workouts, monitor calories, and achieve your goals.</p>
        </div>
      </main>
    </div>
  );
}
