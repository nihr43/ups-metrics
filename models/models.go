package models

import (
	"math/big"
)

type Ups struct {
	Model      string
	Load       *big.Int
	Temp       *big.Int
	Ac_voltage *big.Int
}
