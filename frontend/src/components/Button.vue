<template>
  <button
    :class="[
      'base-button',
      `base-button--${variant}`,
      `base-button--${size}`,
      { 'is-disabled': disabled },
    ]"
    :disabled="disabled"
    @click="handleClick"
  >
    <slot />
  </button>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary', // primary, secondary, danger, etc.
  },
  size: {
    type: String,
    default: 'md', // sm, md, lg
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  icon: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['click'])

function handleClick(event) {
  if (!props.disabled) {
    emit('click', event)
  }
}
</script>

<style scoped>
.base-button {
  border: none;
  cursor: pointer;
  padding: 0.6rem 1rem;
  font-size: 0.95rem;
  border-radius: 6px;
  transition:
    background 0.2s,
    opacity 0.2s;
}

/* Variants */
.base-button--primary {
  background: #4f46e5;
  color: white;
}
.base-button--secondary {
  background: #e5e7eb;
  color: #111827;
}
.base-button--danger {
  background: #dc2626;
  color: white;
}

/* Sizes */
.base-button--sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
}
.base-button--md {
  padding: 0.6rem 1rem;
}
.base-button--lg {
  padding: 0.8rem 1.2rem;
  font-size: 1.05rem;
}

/* Disabled */
.is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
