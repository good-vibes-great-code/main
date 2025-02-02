<script>
    import { onMount } from "svelte";
    import { InfoCircleSolid, ArrowRightOutline, UserCircleSolid, AdjustmentsVerticalOutline, DownloadSolid} from 'flowbite-svelte-icons'
    import { sineIn } from 'svelte/easing';
    import { browser } from "$app/environment";
    import mapboxgl from "mapbox-gl";
    import turf from "turf";
    import "mapbox-gl/dist/mapbox-gl.css"
    import { Accordion, AccordionItem, Drawer, Button, CloseButton , ButtonGroup, Tabs, TabItem} from "flowbite-svelte";
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
    let activeMissions = [];
    let doneMissions = [];
    let shopItems = [];
    let missionTypes = {};
    let landBoundery; // geo json
    let hide_user_drawer = true;
    let transitionParams = {
        x: 320,
        duration: 200,
        easing: sineIn
    };

    const dateFormatter = new Intl.DateTimeFormat('en-US', {
        weekday: 'long', // "Saturday"
        year: 'numeric', // "2025"
        month: 'long', // "February"
        day: 'numeric', // "1"
        hour: 'numeric', // "4"
        });
    mapboxgl.accessToken =
        "pk.eyJ1IjoiZnJhbmt2djE5OTciLCJhIjoiY201cWpwbXM1MDBqbzJrc2U3YzViOXZ6MiJ9.bIR8krCe9RfTQ-5gP7Km7A";

    onMount(async () => {
        dataPromise = fetchData();
        await dataPromise;

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
            const response = await (await fetch(`http://localhost:8000/api/mission_instances/completed_missions/`)).json();
            Object.values(response).forEach(mission => {
                doneMissions.push(mission);
            });
        }
        catch {
            console.log(`Failed to fetch missions`);
        }
        try {
            const response = await (await fetch(`http://localhost:8000/api/mission_instances/active_missions/`)).json();
            Object.values(response).forEach(mission => {
                activeMissions.push(mission);
            });
        }
        catch {
            console.log(`Failed to fetch missions`);
        }
        try {
            const response = await (await fetch(`http://localhost:8000/api/shop/`)).json();
            Object.values(response).forEach(shopItem => {
                shopItems.push(shopItem);
            });
            console.log(shopItems);
        }
        catch {
            console.log(`Failed to fetch shpo`);
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
            {#each activeMissions as mission}
                <AccordionItem>
                    <span slot="header">
                        {missionTypes.find(mType => mType.id === mission.mission_type)?.title || 'Unknown Mission'}
                    </span>
                    <p class="text-gray-500 dark:text-gray-400">
                        {missionTypes.find(mType => mType.id === mission.mission_type)?.description || 'No description available'}
                    </p>
                </AccordionItem>
            {/each}
        </Accordion>
    </div>
    {/await}
</div>
<img class='absolute top-8 right-8 z-10 size-20 opacity-65' src="./user.png" alt="poep" on:click={() => (hide_user_drawer = false)}/>
<Drawer placement="right" transitionType="fly" {transitionParams} bind:hidden={hide_user_drawer} id="sidebar1" width="w-full">
    <Tabs class="*:w-full grid grid-cols-4">
        <TabItem open title="Profile">
            <h2>Completed missions</h2>
            <Accordion>
                {#each doneMissions as mission}
                    <AccordionItem>
                        <span slot="header">
                            <div class="grid grid-cols-2">
                                <div class="text-left">
                                    {missionTypes.find(mType => mType.id === mission.mission_type)?.title || 'Unknown Mission'}
                                </div>
                                <div class="text-right">
                                    Completed on: {mission.completed_at ? dateFormatter.format(new Date(mission.completed_at)) : 'Unknown date'}
                                </div>
                            </div>
                        </span>
                        <p class="text-gray-500 dark:text-gray-400">
                            {missionTypes.find(mType => mType.id === mission.mission_type)?.description || 'No description available'}
                        </p>
                    </AccordionItem>
                {/each}
            </Accordion>
        </TabItem>
        <TabItem title="Points shop">
            <h2>Settings</h2>
            <Accordion>
                {#each shopItems as shopItem}
                    <AccordionItem>
                        <span slot="header">
                            <div class="grid grid-cols-2 w-full">
                                <div class="text-left">
                                    {shopItem.name}
                                </div>
                                <div class="text-right">
                                    {shopItem.price} points
                                </div>
                            </div>
                        </span>
                        <p class="text-gray-500 dark:text-gray-400">
                            {shopItem.description}
                        </p>
                    </AccordionItem>
                {/each}
            </Accordion>
        </TabItem>
        <TabItem title="Wildlife Sighting Statistics">
            <h2>Wildlife Sighting Statistics</h2>
        </TabItem>
        <TabItem title="Achievements">
            <h2>Achievements</h2>
        </TabItem>
    </Tabs>
    <CloseButton on:click={() => (hide_user_drawer = true)} class="top-4 right-8 absolute w-50 mb-4 dark:text-white" />
</Drawer>