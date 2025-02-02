<script>
    import { onMount } from "svelte";
    import { InfoCircleSolid, ArrowRightOutline, UserCircleSolid, AdjustmentsVerticalOutline, DownloadSolid, BuildingSolid, BugSolid, CartSolid, DatabaseSolid, InstagramSolid, TwitterSolid, UsersGroupSolid} from 'flowbite-svelte-icons'
    
    import { Tooltip } from 'flowbite-svelte';

    import { sineIn } from 'svelte/easing';
    import { browser } from "$app/environment";
    import mapboxgl from "mapbox-gl";
    import turf from "turf";
    import "mapbox-gl/dist/mapbox-gl.css"
    import { Accordion, AccordionItem, Drawer, Button, CloseButton , ButtonGroup, Tabs, TabItem} from "flowbite-svelte";
    let map;
    let mapContainer;
    let locationCenter = turf.point([4., 51.]);
    let locationPolygon;
    let tempLocationPolygon;
    let zipcode = "3329 KP";

    // marker collections
    let dataPromise;
    let points = 1200;
    let interventions = [locationCenter] // markers for interventions
    let sightings = [];
    let activeMissions = [];
    let doneMissions = [];
    let shopItems = [];
    let missionTypes = {};
    let landBoundery; // geo json
    let hide_user_drawer = true;
    let hoveredMarker = null;
    let transitionParams = {
        x: 320,
        duration: 200,
        easing: sineIn
    };
    let achievements = [
    { title: "Bob the Builder", description: "Build 10 homes", icon: BuildingSolid, progress: 6, total: 10 },
    { title: "Collector", description: "Invite 10 insects", icon: BugSolid, progress: 3, total: 10 },
    { title: "Big Money, Big Spend", description: "Purchase 10 store items", icon: CartSolid, progress: 3, total: 10 },
    { title: "Bird Watcher", description: "Make 10 sightings", icon: DatabaseSolid, progress: 2, total: 10 },
    { title: "Influencer", description: "Share 10 sightings", icon: InstagramSolid, progress: 9, total: 10 },
    { title: "Birdie", description: "Have 10 different bird species in your garden", icon: TwitterSolid, progress: 1, total: 10 },
    { title: "Collaboration", description: "Invite three neighbours to the program", icon: UsersGroupSolid, progress: 7, total: 10 }
  ];

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
            style: "mapbox://styles/mapbox/satellite-streets-v12",
            center: locationCenter.geometry.coordinates,
            zoom: 9,
        });
        map.on("load", async () => {
            // Load the sighting map markers
            sightings.forEach(sighting => {
                // console.log(sighting.spot_location);
                const lon = sighting.spot_location.split(" ")[1].replace("(","")
                const lat = sighting.spot_location.split(" ")[2].replace(")","")
                const location = turf.point([lon,lat]);
                console.log(location);
                const marker = new mapboxgl.Marker()
                    .setLngLat(location.geometry.coordinates)
                    .addTo(map);
                marker.getElement().addEventListener("mouseenter", () => {
                    const popup = new mapboxgl.Popup({ offset: 25 })
                        .setLngLat(marker.getLngLat())
                        .setHTML(sighting.species_name)
                        .addTo(map);

                    // Close popup when the mouse leaves the marker
                    marker.getElement().addEventListener("mouseleave", () => {
                        popup.remove();
                    });
                });
            });
            doneMissions.forEach(async improvement => {
                const response = await (await fetch(`http://localhost:8000/api/complete_mission/${improvement.id}`)).json();
                console.log(improvement);
                const lon = response.gps_coordinates.split(" ")[1].replace("(","")
                const lat = response.gps_coordinates.split(" ")[2].replace(")","")
                const location = turf.point([lon,lat]);
                const marker = new mapboxgl.Marker({ "color": "#19b402" })
                    .setLngLat(location.geometry.coordinates)
                    .addTo(map);
                marker.getElement().addEventListener("mouseenter", () => {
                    const popup = new mapboxgl.Popup({ offset: 25 })
                        .setLngLat(marker.getLngLat())
                        .setHTML(missionTypes.find(mType => mType.id === improvement.mission_type)?.title || 'Unknown Mission')
                        .addTo(map);

                    // Close popup when the mouse leaves the marker
                    marker.getElement().addEventListener("mouseleave", () => {
                        popup.remove();
                    });
                });
            });
            const popup = new mapboxgl.Popup({
                closeButton: false,
                closeOnClick:false
            });
                
            console.log(locationPolygon)
            map.addSource('erf', {
                'type': 'geojson',
                'data': {
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    // These coordinates outline Maine.
                    'coordinates': [locationPolygon],
                }
            }
            });
            // Add a new layer to visualize the polygon.
            map.addLayer({
                'id': 'erf_layer',
                'type': 'fill',
                'source': 'erf', // reference the data source
                'layout': {},
                'paint': {
                    'fill-color': '#0080ff', // blue color fill
                    'fill-opacity': 0.5
                }
            });
            // console.log(turf.polygon([locationPolygon]))
            const bounds = new mapboxgl.LngLatBounds();
            locationPolygon.forEach(coord => {
                bounds.extend(coord);
            })
            map.fitBounds(bounds, {
                padding: {top: 50, right: 50, left: 50, bottom: 50}
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
            const response = await (await fetch(`http://localhost:8000/api/sightings/`)).json();
            Object.values(response).forEach(sighting => {
                sightings.push(sighting);
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
        try {
            const response = await (await fetch(`http://localhost:8000/api/locations/`)).json();
        
            locationPolygon = parseSRIDPolygon(response[0].boundary);
            tempLocationPolygon = turf.polygon([locationPolygon])
            locationPolygon = [];
            Object.values(tempLocationPolygon.geometry.coordinates[0]).forEach(coordinates => {
                console.log(coordinates);
                locationPolygon.push([coordinates.lng, coordinates.lat])
            });
            
        }
        catch (e){
            console.log(`Failed to fetch location`);
            console.log("Error", e.stack);
    console.log("Error", e.name);
    console.log("Error", e.message);
        }
    }

    function parseSRIDPolygon(polygonString) {
        // Extract the coordinate part using regex
        const match = polygonString.match(/POLYGON \(\((.*)\)\)/);
        if (!match) throw new Error("Invalid POLYGON format");
        
        // Split coordinates and map to an array of unique objects
        const coords = match[1]
            .split(", ")
            .map(coord => {
                const [lng, lat] = coord.split(" ").map(Number);
                return { lng, lat };
            });
        
        // Remove duplicates by using a Set with a JSON string key
        const uniqueCoords = Array.from(new Set(coords.map(JSON.stringify))).map(JSON.parse);
        
        return uniqueCoords;
    }
</script>
<div id="map" bind:this={mapContainer}></div>
<div class="z-10 absolute w-full h-full pointer-events-none">
    <!-- <div class="items-center justify-center p-4 bg-gray-900 text-white rounded-lg shadow-lg">
        <span class="text-2xl font-bold">Points:</span>
        <span class="ml-2 text-3xl font-extrabold text-yellow-400 animate-pulse">{points}</span>
    </div> -->
    <div class="z-10 bg-white rounded-md justify-self-center px-4 mt-3 shadow-lg opacity-90">
        <svg width="200" height="100" viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <defs>
                <linearGradient id="greenGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#4CAF50"/>
                    <stop offset="100%" stop-color="#2E7D32"/>
                </linearGradient>
            </defs>
            <text x="10" y="60" font-family="Arial, sans-serif" font-size="48" font-weight="bold" fill="url(#greenGradient)">ReWild</text>
            <circle cx="170" cy="30" r="10" fill="#4CAF50"/>
            <path d="M 170 30 Q 160 10, 150 30 T 130 30" stroke="#2E7D32" stroke-width="3" fill="none"/>
        </svg>
    </div>
    
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
                    <span slot="header" class="w-full">
                        <div class="grid grid-cols-2 w-full">
                            <div class="text-left">
                                {missionTypes.find(mType => mType.id === mission.mission_type)?.title || 'Unknown Mission'}
                            </div>
                            <div class="text-gray-500 dark:text-gray-400 text-right justify-self-end mr-10">
                                {mission.points} pts
                            </div>
                        </div>

                    </span>
                    <div class="text-gray-500 dark:text-gray-400">
                        {missionTypes.find(mType => mType.id === mission.mission_type)?.description || 'No description available'}
                    </div>
                    
                </AccordionItem>
            {/each}
        </Accordion>
    </div>
    {/await}
</div>
<img class='absolute top-8 right-8 z-10 size-20 opacity-65' src="./user.png" alt="user" on:click={() => (hide_user_drawer = false)}/>
<Drawer placement="right" transitionType="fly" {transitionParams} bind:hidden={hide_user_drawer} id="sidebar1" width="w-full">
    <Tabs class="*:w-full grid grid-cols-4">
        <TabItem open title="Profile">
            <h2>Completed missions</h2>
            <Accordion>
                {#each doneMissions as mission}
                    <AccordionItem>
                        <span slot="header" class="w-full">
                            <div class="grid grid-cols-2">
                                <div class="text-left">
                                    {missionTypes.find(mType => mType.id === mission.mission_type)?.title || 'Unknown Mission'}
                                </div>
                                <div class="text-right justify-self-end mr-10">
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
            <h2>Current points: 600</h2>
            <Accordion>
                {#each shopItems as shopItem}
                    <AccordionItem>
                        <span slot="header" class="w-full">
                            <div class="grid grid-cols-2 w-full">
                                <div class="text-left">
                                    {shopItem.name}
                                </div>
                                <div class="text-right justify-self-end mr-10">
                                    {shopItem.price} pts
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
            <Accordion>
                {#each sightings as sighting}
                    <AccordionItem>
                        <span slot="header" class="w-full">
                            <div class="grid grid-cols-2 w-full">
                                <div class="text-left">
                                    {sighting.species_name}
                                </div>
                                <div class="text-right justify-self-end mr-10">
                                    1 sighting
                                </div>
                            </div>
                        </span>
                        <p class="text-gray-500 dark:text-gray-400">
                            {dateFormatter.format(new Date(sighting.reported_at))}
                        </p>
                    </AccordionItem>
                {/each}
            </Accordion>
        </TabItem>
        <TabItem title="Achievements">
            <h2>Achievements</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
                {#each achievements as achievement}
                  <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md flex flex-col items-center">
                    <!-- <Tooltip content={achievement.description} placement="top"> -->
                        <div class="flex items-center space-x-2 cursor-pointer">
                            <achievement.icon class="w-8 h-8 text-blue-500 dark:text-blue-400" />
                            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{achievement.title}</h3>
                        </div>
                    <Tooltip>
                        {achievement.description}
                    </Tooltip>
                    
                    <!-- </Tooltip> -->
              
                    <!-- Custom Tailwind Progress Bar -->
                    <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 mt-3">
                      <div class="bg-blue-500 h-3 rounded-full transition-all duration-300" style="width: {(achievement.progress / achievement.total) * 100}%"></div>
                    </div>
              
                    <p class="text-sm text-gray-500 mt-2">{achievement.progress} / {achievement.total} Completed</p>
                  </div>
                {/each}
              </div>
        </TabItem>
    </Tabs>
    <CloseButton on:click={() => (hide_user_drawer = true)} class="top-4 right-8 absolute w-50 mb-4 dark:text-white" />
</Drawer>