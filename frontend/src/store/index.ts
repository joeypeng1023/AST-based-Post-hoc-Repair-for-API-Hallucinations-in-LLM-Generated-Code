import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface FixItem {
  line: number
  column: number
  original: string
  corrected: string
  type: string
}

export interface FixResponse {
  fixed_code: string
  fixes: FixItem[]
  status: string
}

export const useCodeStore = defineStore('code', () => {
  const originalCode = ref<string>('')
  const fixedCode = ref<string>('')
  const fixes = ref<FixItem[]>([])
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)
  const fixCount = ref<number>(0)
  const processingTime = ref<number>(0)

  function setOriginalCode(code: string) {
    originalCode.value = code
  }

  function setFixedCode(code: string) {
    fixedCode.value = code
  }

  function setFixes(fixList: FixItem[]) {
    fixes.value = fixList
    fixCount.value = fixList.length
  }

  function setLoading(loading: boolean) {
    isLoading.value = loading
  }

  function setError(err: string | null) {
    error.value = err
  }

  function setProcessingTime(time: number) {
    processingTime.value = time
  }

  function reset() {
    originalCode.value = ''
    fixedCode.value = ''
    fixes.value = []
    isLoading.value = false
    error.value = null
    fixCount.value = 0
    processingTime.value = 0
  }

  return {
    originalCode,
    fixedCode,
    fixes,
    isLoading,
    error,
    fixCount,
    processingTime,
    setOriginalCode,
    setFixedCode,
    setFixes,
    setLoading,
    setError,
    setProcessingTime,
    reset
  }
})