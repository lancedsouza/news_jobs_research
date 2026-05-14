import NewsSidebar from '@/components/NewsSidebar';

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-[#f3f2ef] py-8">
      <div className="max-w-6xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left/Center: The Main Content (Placeholder for now) */}
        <div className="lg:col-span-8">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">Lead Engine 2.0</h1>
            <p className="text-gray-600 italic">Market Intelligence Dashboard</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm min-h-[400px] flex items-center justify-center">
            <p className="text-gray-500">Main Content Area (Scout Agent goes here later)</p>
          </div>
        </div>

        {/* Right: The News Sidebar */}
        <div className="lg:col-span-4">
          <div className="sticky top-8">
            <NewsSidebar />
          </div>
        </div>

      </div>
    </div>
  );
}