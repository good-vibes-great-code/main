<script>
    import { onMount } from "svelte";
    import { InfoCircleSolid, ArrowRightOutline, UserCircleSolid, AdjustmentsVerticalOutline, DownloadSolid} from 'flowbite-svelte-icons'
    import { sineIn } from 'svelte/easing';
    import { browser } from "$app/environment";
    import mapboxgl from "mapbox-gl";
    import turf from "turf";
    import "mapbox-gl/dist/mapbox-gl.css"
    import { Accordion, AccordionItem, Drawer, Button, CloseButton , ButtonGroup} from "flowbite-svelte";
    let map;
    let mapContainer;
    let locationCenter = turf.point([4.741815873559253, 51.78959525586813]);
    let testPoint = turf.point([0.0, 0.0]);
    let zipcode = "3329 KP";

    // marker collections
    let dataPromise;
    let points = 1200;
    let interventions = [locationCenter] // markers for interventions
    let sightingMarkers = [];
    let missions = [];
    let missionTypes = {};
    let landBoundery; // geo json
    let hide_user_drawer = true;
    let transitionParams = {
        x: 320,
        duration: 200,
        easing: sineIn
    };
    mapboxgl.accessToken =
        "pk.eyJ1IjoiZnJhbmt2djE5OTciLCJhIjoiY201cWpwbXM1MDBqbzJrc2U3YzViOXZ6MiJ9.bIR8krCe9RfTQ-5gP7Km7A";

    onMount(async () => {
        dataPromise = fetchData();
        await dataPromise;
        console.log(missions);

        // Render Map
        map = new mapboxgl.Map({
            container: mapContainer,
            style: "mapbox://styles/mapbox/satellite-v9",
            center: locationCenter.geometry.coordinates,
            zoom: 17,
        });        
        
        map.on("load", async () => {
            // Load the intervention map markers
            interventions.forEach(intervention => {
                const marker = new mapboxgl.Marker()
                    .setLngLat(intervention.geometry.coordinates)
                    .addTo(map);
                marker.getElement().addEventListener("click", () => {
                    alert("marker clicked");
                })
            })
        });
    });

    async function fetchData() {
        // Fetch mission types
        try {
            missionTypes = await (await fetch(`http://localhost:8000/api/mission_types/`)).json();
        }
        catch {
            console.log(`Failed to fetch mission types`);
        }
        // Fetch missions
        try {
            const response = await (await fetch(`http://localhost:8000/api/mission_instances/`)).json();
            Object.values(response).forEach(mission => {
                missions.push(mission);
            });
        }
        catch {
            console.log(`Failed to fetch missions`);
        }
    }
</script>
<div id="map" bind:this={mapContainer}></div>
<div class="z-10 absolute w-full h-full pointer-events-none">
    <!-- <div class="items-center justify-center p-4 bg-gray-900 text-white rounded-lg shadow-lg">
        <span class="text-2xl font-bold">Points:</span>
        <span class="ml-2 text-3xl font-extrabold text-yellow-400 animate-pulse">{points}</span>
    </div> -->
    
    {#await dataPromise}
        <p>Waiting on Data</p>
    {:then data} 
    <div class="max-w-sm mt-10 ml-10 p-4 bg-white rounded-lg shadow-md pointer-events-auto">
        <h1 class="text-4xl font-bold text-gray-800 text-center border-b-4 border-blue-500 pb-2">
            Missions
        </h1>
        <Accordion>
            {#each missions as mission}
                <AccordionItem>
                    <span slot="header">{missionTypes[mission['mission_type']]['title']}</span>
                    <p class="text-gray-500 dark:text-gray-400">
                        {missionTypes[mission['mission_type']]['description']}
                    </p>
                </AccordionItem>
            {/each}
        </Accordion>
    </div>
    {/await}
</div>
<img class='absolute top-8 right-8 z-10 size-20 opacity-65' src="./user.png" alt="poep" on:click={() => (hide_user_drawer = false)}/>
<Drawer placement="right" transitionType="fly" {transitionParams} bind:hidden={hide_user_drawer} id="sidebar1" width="w-full">
    <div class="flex items-center">
        <ButtonGroup class="*:w-full grid grid-cols-4">
            <Button>
              <UserCircleSolid class="w-4 h-4 me-2" />
              <h1>Profile</h1>
            </Button>
            <Button>
              <AdjustmentsVerticalOutline class="w-4 h-4 me-2" />
              <h1>Settings</h1>
            </Button>
            <Button>
              <DownloadSolid class="w-4 h-4 me-2" />
              <h1>Download</h1>
            </Button>
          </ButtonGroup>
      <CloseButton on:click={() => (hide_user_drawer = true)} class="w-50 mb-4 dark:text-white" />
    </div>
    <p class="mb-6 text-sm text-gray-500 dark:text-gray-400">
      Supercharge your hiring by taking advantage of our <a href="/" class="text-primary-600 underline dark:text-primary-500 hover:no-underline"> limited-time sale </a>
      for Flowbite Docs + Job Board. Unlimited access to over 190K top-ranked candidates and the #1 design job board.
    </p>
    <div class="grid grid-cols-2 gap-4">
      <Button color="light" href="/">Learn more</Button>
      <Button href="/" class="px-4">Get access <ArrowRightOutline class="w-5 h-5 ms-2" /></Button>
    </div>
  </Drawer>