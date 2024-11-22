import { useSignal } from "@preact/signals";
import Map from "../islands/Map.tsx";


export default function Home() {
  const myAPIKey = useSignal(Deno.env.get('GEOAPIFY_API_KEY'));
  
  return (
    <div class="bg-[#86efac]">
      <div class={"flex items-center w-1/4"}>
        <a class={"inline-block"} href={"/"}>
          <img src="/marvin.png" class={""} alt="marvin-logo-by-pngegg" />
        </a>
        <a class={"inline-block"} href={"/"}>
          <h1 class="mx-2 text-xl my-2 font-bold">GMME - GUIA DO MOCHILEIRO DAS MORADIAS ESTUDANTIS</h1>
        </a>
      </div>
      <div class="mx-auto flex flex-col items-center justify-center">
        <div class="flex justify-center items-center">
          <p class="text-xl text-center">
          Conseguiu a sonhada aprovação e precisa se mudar, calouro(a)?
          <br />Quer encontrar um lugar novo com <span class="bold text-red-700">rapidez</span>, veterano(a)?!
          <br/>Então, você está no lugar certo!!!
          </p>
          <img class="p-2" height="15%" width="15%" src="/dontpanic.png" alt="dontpanic" />
        </div>
        <p class={"text-xl mt-6 font-semibold"}>Encontre um lugar com o custo-benefício ideal que você merece agora mesmo, estudante!</p>
        {/* <h2 class="text-xl">Encontre  para você que quer morar próximo à sua universidade!</h2> */}
        <Map myAPIKey={myAPIKey}/>
      </div>
    </div>
  );
}
