<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <header>
        <nav id="menu">
            <RouterLink to="/">Domů</RouterLink>
            <RouterLink to="/about">O nás</RouterLink>
        </nav>
    </header>

    <RouterView />

</template>
