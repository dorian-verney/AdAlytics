<script>
    // Example histogram data
    let data = [5, 10, 7, 12, 6, 9, 4];
  </script>
  
  <div class="bg-white shadow rounded-md p-6 flex flex-col items-center justify-center">
    <h2 class="text-lg font-semibold mb-4">Metrics Histogram</h2>
    <div class="w-full flex items-end space-x-2 h-40">
      {#each data as value}
        <div
          class="bg-blue-500 w-6 rounded-t-md transition-all"
          style="height: {value * 25}px"
          title={value}
        ></div>
      {/each}
    </div>
  </div>
  