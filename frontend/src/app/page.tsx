import QueryAssistant from "@/components/QueryAssistant";

export default function HomePage() {
  return (
    <main className="p-4 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Query Assistant</h1>
      <QueryAssistant />
    </main>
  );
}
