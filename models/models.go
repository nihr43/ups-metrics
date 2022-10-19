package models

import (
	"math/big"
)

type ups struct {
	Model      string
	Load       *big.Int
	Temp       *big.Int
	Ac_voltage *big.Int
}
