import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { describe, expect, it } from 'vitest'

const specPath = resolve(__dirname, '../..', 'spec.yaml')
const specText = readFileSync(specPath, 'utf-8')

describe('spec.yaml', () => {
  it('mUST exist', () => {
    expect(specText).toBeTruthy()
  })

  it('mUST have schema 1.0', () => {
    const yaml = require('yaml')
    const data = yaml.parse(specText)
    expect(data.schema).toBe('1.0')
  })

  it('mUST be version 1.2.0', () => {
    const yaml = require('yaml')
    const data = yaml.parse(specText)
    expect(data.version).toBe('1.2.0')
  })

  it('mUST be web_fullstack', () => {
    const yaml = require('yaml')
    const data = yaml.parse(specText)
    expect(data.project.type).toBe('web_fullstack')
  })

  it('mUST reference architecture, devops, testing, security', () => {
    const yaml = require('yaml')
    const data = yaml.parse(specText)
    const refs = data.references.items
    expect(refs).toContain('architecture')
    expect(refs).toContain('devops')
    expect(refs).toContain('testing')
    expect(refs).toContain('security')
  })
})

it('mUST include farmer-visual-style reference', () => {
  const yaml = require('yaml')
  const data = yaml.parse(specText)
  const refs = data.references?.items ?? []
  expect(refs).toContain('farmer-visual-style')
})

it('mUST define themes.visual_style with allowed baseline+farmer', () => {
  const yaml = require('yaml')
  const data = yaml.parse(specText)
  expect(data.themes?.visual_style?.allowed).toEqual(['farmer', 'baseline'])
})
