import { useState } from 'react'
import { Option, OptionData } from './components/Option'
import {
  Button,
  Title,
  Box,
  Container,
  Textarea,
  Select,
  Group,
  TextInput,
  Slider
} from '@mantine/core'
import { notifications } from '@mantine/notifications'

function App () {
  const [question, setQuestion] = useState<string | undefined>(undefined)
  const [answerType, setAnswerType] = useState<string>('options')

  const [options, setOptions] = useState<OptionData[]>([])
  const [correctAnswer, setCorrectAnswer] = useState<string | undefined>(undefined)

  const [isUploading, setIsUploading] = useState(false)
  const [difficulty, setDifficulty] = useState(0)

  const addOption = () => {
    setOptions(options.concat({value: '', isCorrect: false} as OptionData))
  }

  const setOption = (value: OptionData, index: number) => {
    const localOptions: any[] = Object.assign([], options)
    localOptions[index] = value
    setOptions(localOptions)
  }

  const submitTask = () => {
    if (question === undefined) {
      notifications.show({
        color: 'red',
        title: 'Ошибка валидации!',
        message: 'Не указан вопрос задания.',
      })
      return
    }

    if (answerType === 'text' && correctAnswer == undefined) {
      notifications.show({
        color: 'red',
        title: 'Ошибка валидации!',
        message: 'Не указан правильный ответ на задание.',
      })
      return
    }

    const emptyOption = options.findIndex(val => !val.value)

    if (emptyOption !== -1) {
      notifications.show({
          color: 'red',
          title: 'Ошибка валидации!',
          message: `Ответ №${emptyOption + 1} не имеет никакого текста в качестве ответа.`,
        })
      return
    }

    let isSet = false
    let isValidationError = false

    options.find((val, index) => {
      if (val.isCorrect) {
        if (isSet) {
          notifications.show({
            color: 'red',
            title: 'Ошибка валидации!',
            message: `Существует как минимум два варианта ответа, помеченные как правильные. Данная ошибка возникла в варианте ответа №${index + 1}.`,
          })
          isValidationError = true
          return
        }

        isSet = true
      }
    })

    if (isValidationError) {
      return
    }

    if (!isSet && answerType === 'options') {
      notifications.show({
        color: 'red',
        title: 'Ошибка валидации!',
        message: 'Не существует ни одного варианта ответа, который был бы отмечен как правильный.',
      })
      return
    }

    // TODO: send to API

    notifications.show({
      color: 'blue',
      loading: true,
      autoClose: false,
      withCloseButton: false,
      id: 'uploading-status',
      title: 'Пожалуйста, подождите...',
      message: 'Производится загрузка Вашего задания на сервер...',
    })

    setIsUploading(true)

    const body = new URLSearchParams()
    body.append('body', question)
    body.append('complexity', difficulty.toString())
    body.append('answer', correctAnswer!!)

    // TODO: api doesn't support options now

    fetch('http://127.0.0.1:5000/questions', {
      method: 'POST',
      body,
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => response.json())
    .then((response) => {
      notifications.update({
        color: 'green',
        autoClose: true,
        withCloseButton: true,
        id: 'uploading-status',
        title: 'Задание загружено!',
        message: 'Ваше задание успешно загружено на сервер!',
      })
      setIsUploading(false)
    })
    .catch((err) => {
      notifications.update({
        color: 'red',
        autoClose: true,
        withCloseButton: true,
        id: 'uploading-status',
        title: 'Произошла ошибка!',
        message: 'Что-то пошло не так....',
      })
      setIsUploading(false)
    })

    // setTimeout(() => {
    //   notifications.update({
    //     color: 'green',
    //     autoClose: true,
    //     withCloseButton: true,
    //     id: 'uploading-status',
    //     title: 'Задание загружено!',
    //     message: 'Ваше задание успешно загружено на сервер!',
    //   })
    // }, 10000)
  }

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
            onChange={event => setQuestion(event.currentTarget.value)}
            required
          />
        </Box>
        <Box mt='md'>
          <Select
            label='Тип ответа'
            placeholder='Выберите тип ответа на задачу'
            data={[
              { value: 'text', label: 'Тектовый ответ' },
              { value: 'options', label: 'Ответ на викторину' }
            ]}
            value={answerType}
            onChange={(e) => setAnswerType(e!!)}
            required
          />
        </Box>
        <Box mt='md'>
          {answerType ? (
            answerType === 'text' ? (
              <TextInput
                required
                value={correctAnswer}
                label='Правильный ответ'
                onChange={(e) => setCorrectAnswer(e.currentTarget.value)}
              />
            ) : (
              <Group>
                <Button onClick={addOption}>Добавить ответ</Button>
                {options.map((item, index) => (
                  <Option
                    key={index}
                    
                    optionValue={item.value!!}
                    isCorrectAnswer={item.isCorrect}

                    onCorrectAnswerChange={(v) => setOption({isCorrect: v, value: options[index].value}, index)}
                    onOptionValueChange={(v) => setOption({isCorrect: options[index].isCorrect, value: v}, index)}

                    onDelete={() => {
                      setOptions((oldOptions) => {
                        return oldOptions.filter((_, i) => i !== index)
                      })
                    }}
                  />
                ))}
              </Group>
            )
          ) : (
            ''
          )}
        </Box>
        <Box mt='md'>
          <Slider
            min={0}
            max={5}
            step={1}
            marks={[
              { value: 0, label: 'Очень легко' },
              { value: 1, label: 'Легко' },
              { value: 2, label: 'Средне' },
              { value: 3, label: 'Сложно' },
              { value: 4, label: 'Очень сложно' },
              { value: 5, label: 'Невероятно сложно' },
            ]}
            onChange={(e) => setDifficulty(e)}
          />
        </Box>
        <Box mt='xl'>
          <Button
            onClick={submitTask}
            disabled={isUploading}
          >
            Отправить задание
          </Button>
        </Box>
      </Box>
    </Container>
  )
}

export default App
