<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ref } from 'vue';
import InputText from 'primevue/inputtext';

const {t} = useI18n();
const sidePanelVisible = ref(false);
const api_key = ref('');

</script>

<template>
    <v-card>
    <v-layout>
      <div class="card flex justify-content-center">
        <Sidebar v-model:visible="sidePanelVisible" header="Settings">
          <div class="flex flex-column gap-2">
            <small id="username-help">Enter your Api Key.</small>
            <InputText id="api_key" v-model="api_key" aria-describedby="api_key-help" />
          </div>
        </Sidebar>
      </div>     
       <v-main>
        <v-card>
          Policy Summarization App
          <Button icon="pi pi-arrow-right" @click="sidePanelVisible = true" />
        </v-card>
      </v-main>
    </v-layout>
  </v-card>
</template>

<style scoped>

</style>
