<script setup>
import BookIcon from '@/assets/book-icon.svg'
</script>

<template>
  <nav class="navbar">
    <div class="brand">MyApp</div>

    <ul class="links">
      <li>
        <img :src="BookIcon" />
        <span>
          <RouterLink to="/disciplinas">Disciplinas</RouterLink>
        </span>
        <span>
          <RouterLink to="/calendario">Calendario</RouterLink>
        </span>
        <span>
          <RouterLink to="/relatorios">Relatorios</RouterLink>
        </span>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
.navbar {
  background: linear-gradient(to right, #915fed, #5c26bf, #3d79f2);
  padding: 12px 24px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

* {
  color: white;
}

.brand {
  font-size: 1.4rem;
  font-weight: bold;
}

.links {
  list-style: none;
  display: flex;
  gap: 24px;
}

.links li span {
  color: white;
  transition: color 0.2s;
  padding: 0.5em 1em;
  border-radius: 10px;
}

.links li span:hover {
  background-color: white;
}

.links li span:hover a {
  background-image: linear-gradient(to right, #915fed, #5c26bf, #3d79f2);
  background-clip: text;
  color: transparent;
}

@media (max-width: 768px) {
  .links {
    position: absolute;
    top: 64px;
    left: 0;
    width: 100%;
    background: #ffffff;
    flex-direction: column;
    gap: 16px;
    padding: 16px 24px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    display: none;
  }

  .links.open {
    display: flex;
  }
}
</style>
