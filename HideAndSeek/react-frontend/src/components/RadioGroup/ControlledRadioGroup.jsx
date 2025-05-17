import {FormControl, FormControlLabel, FormLabel, Radio, RadioGroup} from "@mui/material";

function ControlledRadioGroup({id, label, value, onChange, values, labels}) {
    return (
        <FormControl>
            <FormLabel id={id}>{label}</FormLabel>
            <RadioGroup
                value={value}
                onChange={onChange}
            >
                {
                    values.map((v, i) => (
                        <FormControlLabel
                            key={i}
                            value={v}
                            control={<Radio />}
                            label={labels[i]}
                        />
                    ))
                }
            </RadioGroup>
        </FormControl>
    )
}

export default ControlledRadioGroup