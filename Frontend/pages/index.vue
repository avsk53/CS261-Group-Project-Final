<template>
  <div id="pages" style="height: 100vh;">

    <div>
      <b-jumbotron class="jumbo bg-dark text-light" >
        <template #header>Software Tracker</template>
    
        <template #lead>
          A simple software tracking application for your business. To keep manage and track ongoing software projects. 
        </template>
      </b-jumbotron>
    </div>
    <div class="d-flex justify-content-center align-items-center">
      <Login/>
    </div>
    
  </div>
</template>


<script>
export default {
  name: 'IndexPage',
  layout: 'login_layout', 
  middleware: ['guest'],

}
</script>

<style>
  #pages {
    display: flexbox;
    flex-flow: column wrap;
    justify-content: center;
    align-items: flex-start;
  }
  .jumbo {
    font-family: inherit;
    border-radius: 0;
  }
</style>
