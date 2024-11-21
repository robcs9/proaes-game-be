import { useSignal } from "@preact/signals";
import Map from "../islands/Map.tsx";


export default function Home() {
  const myAPIKey = useSignal(Deno.env.get('GEOAPIFY_API_KEY'));
  
  return (
    <div class="px-4 py-8 mx-auto bg-[#86efac]">
      <div class="max-w-screen-md mx-auto flex flex-col items-center justify-center">
        <h1 class="text-xl font-bold">GMME MAP</h1>
        <Map myAPIKey={myAPIKey}/>
      </div>
    </div>
  );
}
