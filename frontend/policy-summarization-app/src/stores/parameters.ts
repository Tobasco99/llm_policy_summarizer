import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useParametersStore = defineStore('parameters', () => {
  const openAiApiKey = ref('')
  const chunkSize = ref(0)
  function updateOpenAiApiKey(newKey: string) {
    openAiApiKey.value = newKey
  }
  function updateChunkSize(newSize: number) {
    chunkSize.value = newSize
  }

  return { openAiApiKey, chunkSize, updateOpenAiApiKey, updateChunkSize }
})