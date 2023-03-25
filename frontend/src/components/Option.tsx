import { useState } from 'react'
import { Grid, Group, TextInput, Checkbox, Flex } from '@mantine/core'

export const Option = (props: OptionProps) => {
  const [optionValue, setOptionValue] = useState<string>('')
  const [correctAnswer, setCorrectAnswer] = useState<boolean>(false)
  
  return (
    <Grid w={'100%'} span={24}>
      <Grid.Col span={11}>
        <TextInput
          placeholder='Вариант ответа'
          value={optionValue}
          onChange={(event) => setOptionValue(event.currentTarget.value)}
          required
        />
      </Grid.Col>
      <Grid.Col span={1}>
        <Flex justify="center" align="center">
          <Checkbox
            value={correctAnswer}
            onChange={(_event) => setCorrectAnswer(!correctAnswer)}
          />
        </Flex>
      </Grid.Col>
    </Grid>
  )
}
