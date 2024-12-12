import type { Signal } from "@preact/signals";
import { Button } from "../components/Button.tsx";
// import maplibre/plotly here
// import Plotly from "plotly.js-dist"
// import Plotly from "react-plotly"
// console.log(Plotly)
// import { createRef } from "https://esm.sh/v128/preact@10.22.0/src/index.js";
// const ref = createRef()

interface MapProps {
  myAPIKey: Signal<string|undefined>;
}

// let url = `https://maps.geoapify.com/v1/styles/klokantech-basic/style.json?apiKey=${myAPIKey}`;

// Plotly.newPlot()

export default function Map(props: MapProps) {
  
  return (
    <div class="py-6">
      {/* <iframe src="https://www.google.com/maps/d/embed?mid=1q8kcKbPxXyk1U9CmvG68f4nuUkafmV0&hl=en&ehbc=2E312F" width="800" height="600"></iframe> */}
      <iframe src="/map.html" width="800" height="600"></iframe>
      {/* <iframe src="/plot.html" width="800" height="600"></iframe> */}
      {/* <div id="tester" class="w-[600px] h-[250px]"></div>
      <Plotly
        data={[ { x: ['Apples', 'Oranges', 'Bananas'], y: [10, 15, 7], type: 'bar' } ]} layout={{ title: 'Fruit Amount' }}
      /> */}
      {/* <Foo /> */}
    </div>
  );
}
