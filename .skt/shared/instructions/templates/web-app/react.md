# React Rules

## Component Patterns

### Functional Components

**Rule**: Always use functional components with hooks

**Example**:

```typescript
// ✅ Good
export const Component: FC<Props> = ({ data }) => {
  const [state, setState] = useState(initialState)
  return <div>{data}</div>
}

// ❌ Bad - class components
class Component extends React.Component {
  render() {
    return <div>{this.props.data}</div>
  }
}
```

### Props Interface

**Rule**: Define explicit Props interface

**Example**:

```typescript
interface ComponentProps {
  title: string
  onClose: () => void
  children?: React.ReactNode
}

export const Component: FC<ComponentProps> = ({ title, onClose, children }) => {
  return <div>{title}</div>
}
```

## Hooks

### Custom Hooks

**Rule**: Extract reusable logic into custom hooks

**Example**:

```typescript
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key)
    return stored ? JSON.parse(stored) : initialValue
  })
  
  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value))
  }, [key, value])
  
  return [value, setValue] as const
}
```

### Effect Dependencies

**Rule**: Always specify correct dependencies

**Example**:

```typescript
// ✅ Good
useEffect(() => {
  fetchData(userId)
}, [userId])

// ❌ Bad - missing dependency
useEffect(() => {
  fetchData(userId)
}, [])
```

## State Management

### Local State

**Rule**: Keep state as local as possible

**Example**:

```typescript
// ✅ Good - state in component that uses it
function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

### Derived State

**Rule**: Don't store derived state, compute it

**Example**:

```typescript
// ✅ Good
function UserList({ users }: Props) {
  const activeUsers = users.filter(u => u.active)
  return <div>{activeUsers.length} active</div>
}

// ❌ Bad - storing derived state
function UserList({ users }: Props) {
  const [activeUsers, setActiveUsers] = useState([])
  
  useEffect(() => {
    setActiveUsers(users.filter(u => u.active))
  }, [users])
}
```
