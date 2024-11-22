import type { Signal } from "@preact/signals";
import { Button } from "../components/Button.tsx";

interface MapProps {
  myAPIKey: Signal<string|undefined>;
}

// let url = `https://maps.geoapify.com/v1/styles/klokantech-basic/style.json?apiKey=${myAPIKey}`;


export default function Map(props: MapProps) {
  return (
    <div class="py-6">
      <iframe src="https://www.google.com/maps/d/embed?mid=1q8kcKbPxXyk1U9CmvG68f4nuUkafmV0&hl=en&ehbc=2E312F" width="800" height="600"></iframe>
    </div>
  );
}
