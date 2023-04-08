import { Grid, TextInput, Checkbox, Flex, Center, Button, CloseButton } from '@mantine/core'

export interface OptionData {
  value: string,
  isCorrect: boolean,
}

export interface OptionChangeProps {
  optionValueChange: (v: string) => void,
  correctAnswerChange: (v: boolean) => void,
}

export interface OptionProps {
  optionValue: string,
  isCorrectAnswer: boolean,

  onOptionValueChange: (v: string) => void,
  onCorrectAnswerChange: (v: boolean) => void,

  onDelete: () => void,
}

export const Option = (props: OptionProps) => {
  
  return (
    <Grid
      columns={32}
      w='100%'
    >
      <Grid.Col span={2}>
        <Center
          w='100%'
          h='100%'
        >
          <CloseButton 
            size='lg'
            color='red'
            onClick={props.onDelete}
          />
        </Center>
      </Grid.Col>
      <Grid.Col span={28}>
        <TextInput
          placeholder='Вариант ответа'
          value={props.optionValue}
          onChange={(e) => props.onOptionValueChange(e.currentTarget.value)}
          required
        />
      </Grid.Col>
      <Grid.Col span={2}>
        <Center
          w='100%'
          h='100%'
        >
          <Checkbox
            checked={props.isCorrectAnswer}
            onChange={(e) => props.onCorrectAnswerChange(e.currentTarget.checked)}
          />
        </Center>
      </Grid.Col>
    </Grid>
  )
}
