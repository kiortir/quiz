import { useState } from 'react'
import { Option } from './components/Option'
import { MantineProvider, Button, Title, Center, Box, Container, Textarea, Select, Group, TextInput } from '@mantine/core'

/*
{
  "type": "options",
  "body": {
    "question": "2 + 2",
    "answer": "4",
    "options": [
      "4", "5", "6", "3"
    ]
  },
  "difficulty": 5
}
*/

function App() {
  const [question, setQuestion] = useState<string | undefined>(undefined)
  const [answerType, setAnswerType] = useState<string | null>(null)

  return (
    <Container mt='xl'>
      <Box mb='xl'>
        <Title order={2}>Добавление нового задания</Title>
      </Box>
      <Box>
        <Box>
          <Textarea
            label='Введите вопрос задания'
            value={question}
            onChange={(event) => setQuestion(event.currentTarget.value)}
            required
          />
        </Box>
        <Box mt='md'>
          <Select
            label='Тип ответа'
            placeholder='Выберите тип ответа на задачу'
            data={[
              { value: 'text', label: 'Тектовый ответ' },
              { value: 'options', label: 'Ответ на викторину' },
            ]}
            value={answerType}
            onChange={setAnswerType}
            required
          />
        </Box>
        <Box mt='md'>
          {
            answerType ?
              answerType === 'text' ?
                <TextInput
                  label='Правильный ответ'
                  required
                />
              :
                <Group>
                  {/* <Button>
                    Добавить ответ
                  </Button> */}
                  <Option

                  />
                </Group>
            : ''
          }
        </Box>
      </Box>
    </Container>
  )
}

export default App
