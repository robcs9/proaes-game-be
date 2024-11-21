import type { Signal } from "@preact/signals";
import { Button } from "../components/Button.tsx";

interface MapProps {
  myAPIKey: Signal<string|undefined>;
}

// let url = `https://maps.geoapify.com/v1/styles/klokantech-basic/style.json?apiKey=${myAPIKey}`;


export default function Map(props: MapProps) {
  return (
    <div class="flex gap-8 py-6">
      <p class="text-lg">map goes here {props.myAPIKey}</p>
    </div>
  );
}
