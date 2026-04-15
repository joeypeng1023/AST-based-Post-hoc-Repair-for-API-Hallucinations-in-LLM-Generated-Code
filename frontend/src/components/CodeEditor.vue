<template>
  <div class="code-editor" ref="editorContainer"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as monaco from 'monaco-editor'
import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker'
import jsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker'
import cssWorker from 'monaco-editor/esm/vs/language/css/css.worker?worker'
import htmlWorker from 'monaco-editor/esm/vs/language/html/html.worker?worker'
import tsWorker from 'monaco-editor/esm/vs/language/typescript/ts.worker?worker'

interface FixHighlight {
  line: number
  column: number
  original: string
  corrected: string
  type: string
}

interface Props {
  modelValue: string
  language?: string
  readonly?: boolean
  highlights?: FixHighlight[]
}

const props = withDefaults(defineProps<Props>(), {
  language: 'python',
  readonly: false,
  highlights: () => []
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'change', value: string): void
}>()

const editorContainer = ref<HTMLElement | null>(null)
let editor: monaco.editor.IStandaloneCodeEditor | null = null
let decorations: string[] = []

// Initialize workers
self.MonacoEnvironment = {
  getWorker(_, label) {
    if (label === 'json') {
      return new jsonWorker()
    }
    if (label === 'css' || label === 'scss' || label === 'less') {
      return new cssWorker()
    }
    if (label === 'html' || label === 'handlebars' || label === 'razor') {
      return new htmlWorker()
    }
    if (label === 'typescript' || label === 'javascript') {
      return new tsWorker()
    }
    return new editorWorker()
  }
}

onMounted(() => {
  if (editorContainer.value) {
    editor = monaco.editor.create(editorContainer.value, {
      value: props.modelValue,
      language: props.language,
      theme: 'vs-light',
      readOnly: props.readonly,
      automaticLayout: true,
      minimap: { enabled: false },
      fontSize: 14,
      lineNumbers: 'on',
      scrollBeyondLastLine: false,
      renderWhitespace: 'none',
      wordWrap: 'on'
    })

    editor.onDidChangeModelContent(() => {
      if (editor) {
        const value = editor.getValue()
        emit('update:modelValue', value)
        emit('change', value)
      }
    })
  }
})

onBeforeUnmount(() => {
  if (editor) {
    editor.dispose()
  }
})

watch(() => props.modelValue, (newVal) => {
  if (editor && newVal !== editor.getValue()) {
    editor.setValue(newVal)
  }
})

watch(() => props.language, (newLang) => {
  if (editor) {
    monaco.editor.setModelLanguage(editor.getModel()!, newLang)
  }
})

watch(() => props.highlights, (newHighlights) => {
  if (editor && newHighlights.length > 0) {
    applyHighlights(newHighlights)
  }
}, { deep: true })

const applyHighlights = (highlights: FixHighlight[]) => {
  if (!editor) return

  const newDecorations = highlights.map((highlight) => ({
    range: new monaco.Range(
      highlight.line,
      highlight.column,
      highlight.line,
      highlight.column + highlight.original.length
    ),
    options: {
      inlineClassName: 'highlight-fix',
      hoverMessage: {
        value: `**Fix:** \`${highlight.original}\` → \`${highlight.corrected}\`\n**Type:** ${highlight.type}`
      }
    }
  }))

  decorations = editor.deltaDecorations(decorations, newDecorations)
}

defineExpose({
  editor
})
</script>

<style scoped>
.code-editor {
  width: 100%;
  height: 100%;
  min-height: 400px;
}
</style>

<style>
.highlight-fix {
  background-color: #fff3cd;
  border-radius: 2px;
  padding: 2px 0;
  cursor: pointer;
}

.highlight-fix:hover {
  background-color: #ffc107;
}
</style>